import time
from microsquad.game.customeeze.game import Customeeze

from rx3.subject import Subject
import microsquad.gateway.dummy.dummy_gateway as dummy


def main():
    dummy.main()
    game = Customeeze(dummy.gateway.event_source, dummy.gateway.deviceGateway)
    time.sleep(0.5)
    dummy.gateway.connector.simulate_message("read_button,button=\"a\",dev_id=1564566 123456978")
    dummy.gateway.connector.simulate_message("read_button,button=\"a\",dev_id=1564566 123456980")
    dummy.gateway.connector.simulate_message("read_button,button=\"a\",dev_id=1564566 123456982")
    dummy.gateway.connector.simulate_message("read_button,button=\"a\",dev_id=1564566 123456995")
    dummy.gateway.connector.simulate_message("read_button,button=\"b\",dev_id=1564566 123456995")
    dummy.gateway.connector.simulate_message("read_button,button=\"b\",dev_id=1564566 123456995")
    while True:
        time.sleep(5)



if __name__ == "__main__":
    main()