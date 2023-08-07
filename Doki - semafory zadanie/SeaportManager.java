public interface SeaportManager {

    void init(int numberOfDocks, int seawayCapacity);

    void requestSeawayEntrance(Ship s) throws InterruptedException;

    int requestPortEntrance(Ship s) throws InterruptedException;

    void signalPortEntered(Ship s);

    void requestPortExit(Ship s) throws InterruptedException;

    void signalPortExited(Ship s);

    void signalShipSailedAway(Ship s);
}
