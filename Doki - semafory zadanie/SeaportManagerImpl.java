// Pawel Ostrowski
import java.util.concurrent.Semaphore;


public class SeaportManagerImpl implements SeaportManager{

    private Semaphore OpenDocks;
    private Semaphore Seaway;
    private Semaphore arrayUsage;

    private Ship docksTaken[];
    private int docksize;

    public void init(int numberOfDocks, int seawayCapacity)
    {
        docksTaken = new Ship[numberOfDocks];
        docksize = numberOfDocks;
        arrayUsage = new Semaphore( 1, true);
        Seaway = new Semaphore( seawayCapacity, true );
        OpenDocks = new Semaphore( 1, true);
    }

    public void requestSeawayEntrance (Ship s)
    {
        try {
            OpenDocks.acquire();
        } catch (InterruptedException e1) {}

        try {
            Seaway.acquire();
        } catch (InterruptedException e) {}
        
        while (!insertShip(s))
        {

        }
        OpenDocks.release();
    }

    public int requestPortEntrance(Ship s)
    {
        try {
            arrayUsage.acquire();
        } catch (InterruptedException e) {}

        int dock = 0;
        for (int i = 0; i < docksize; i++)
        {            
            if (docksTaken[i] == s)
            {
                dock = i;
                break;
            }
        }
        arrayUsage.release();
        return dock;
    }

    public void signalPortEntered(Ship s)
    {
        Seaway.release();

    }

    public void requestPortExit(Ship s)
    {
        try {
        Seaway.acquire();
        } catch (InterruptedException e) {}
    }

    public void signalPortExited(Ship s)
    {
        try {
            arrayUsage.acquire();
        } catch (InterruptedException e) {}

        int currentI = s.getAssignedDock();
        for (int i = currentI; i < currentI + s.getDockingSize(); i++)
        {
            docksTaken[i] = null;
        }

        arrayUsage.release();
    
    }

    public void signalShipSailedAway(Ship s)
    {
        Seaway.release();
    }

    public boolean insertShip(Ship s)
    {
        boolean inserted = false;
        int currentI = 0;
        int currentLen = 0;

        try {
            arrayUsage.acquire();
        } catch (InterruptedException e) {}


        for (int i = 0; i < docksize; i++)
        {
            if (docksTaken[i] == null)
            {
                currentLen++;
                if (currentLen == s.getDockingSize())
                {
                    inserted = true;
                    break;
                }
            }
            else
            {
                currentLen = 0;
                currentI = i + 1;
            }
        }

        if (inserted)
        {
            for (int i = currentI; i < s.getDockingSize() + currentI; i++)
            {
                docksTaken[i] = s;
            }
        }

        arrayUsage.release();

        return inserted;
    }
}

