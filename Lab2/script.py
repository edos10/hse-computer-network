import icmplib
import logging
import socket
from argparse import ArgumentParser


def InitArgumentsCmd() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(usage="usage")
        
    parser.add_argument("target", type=str, help="Required argument for target machine: IP or hostname.")
    parser.add_argument("-U", "--maxsize", type=int, default=65535, help="Max possible packet size for pings.")
    parser.add_argument("-D", "--minsize", type=int, default=28, help="Min possible packet size for pings.")
    parser.add_argument("-i", "--interval", type=float, default=0.01, help="Interval between pings.")
    parser.add_argument("-t", "--timeout", type=float, default=1, help="Timeout for each ping to target machine.")
    parser.add_argument("-p", "--pings", type=int, default=1, help="Count of pings for one attempt.")
    parser.add_argument("-s", "--show", action="store_true", default=0, help="Showing info in process finding MTU.")

    return parser


class Config:
    size_ip: int = 8
    size_icmp: int = 20


class MTU:
    def __init__(self, source: str, args) -> None:
        self.size_headers: int = Config.size_ip + Config.size_icmp
        self.host: str = socket.gethostbyname(source)
        self.args = args
        if args.show:
            logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
            logging.getLogger().setLevel(logging.INFO)

    def request(self, packet_size: int) -> bool:
        res = icmplib.ping(self.host,
                               interval=self.args.interval,
                               timeout=self.args.timeout,
                               count=self.args.pings,
                               payload_size=packet_size-28)
        logging.info(f"\n----------\nSended {packet_size} bytes. \nAfter ping:\nLoss: {res.packet_loss}\nReceived: {res.packets_received}\n----------")
        return res.is_alive
    

    def calculate(self) -> int:
        # binary search on packet size
        left: int = self.args.minsize - 1
        right: int = self.args.maxsize + 1
        while left < right - 1:
            middle: int = (left + right) // 2
            res_ping: bool = self.request(middle)
            str_res: str = "succeeded" if res_ping else "failed"
            logging.info(f"result of ping with packet size = {middle} is {str_res} to {self.host}")
            if res_ping:
                left = middle
            else:
                right = middle
        
        return left


def main():
    argparser: ArgumentParser = InitArgumentsCmd()
    args = argparser.parse_args()

    ###
    if args.minsize < 28 or args.maxsize > 65535:
        print(f"Wrong size of packets, please setup min and max sizes in [28, 65535].")
        exit(1)
    
    if args.timeout <= 0.001:
        print("Wrong value of timeout for pings. Set up it on value > 0.001")
        exit(2)
    
    if args.interval > 100:
        print("Too long interval, please, try again with value <= 100")
        exit(3)
    
    if args.interval < 0:
        print("Wrong value in interval, please try with value >= 0")
        exit(4)
    ###

    try:
        res = MTU(args.target, args).calculate()
        print(f"MTU was found successfully for host {args.target}, value is {res}")
    except socket.gaierror as e:
        print(f"Error in parameter 'target': wrong IP or hostname.\nRequired correct IP or hostname, try again. \nError: {str(e)}")
    except Exception as e:
        print(f"Error in finding MTU process: {str(e)}.\nTry again later or with another parameters.")


if __name__ == "__main__":
    main()
