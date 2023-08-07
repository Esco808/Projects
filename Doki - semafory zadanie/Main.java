class Ship{
    int size;
    int id;
    Integer assignedDock;
    Ship(int sizeArg, int idArg){
        size = sizeArg;
        id = idArg;
        assignedDock = null;
    }
    public int getDockingSize() {
        return size;
    }

    public void setAssignedDock(int dock) {
        assignedDock = Integer.valueOf(dock);
    }

    public Integer getAssignedDock() {
        return assignedDock;
    }
}

public class Main {

    static class MyThread implements Runnable{
        Ship s;
        SeaportManagerImpl seaport;
        MyThread(Ship sArg, SeaportManagerImpl seaportArg){
            s = sArg;
            seaport = seaportArg;
        }
        public void run(){
            seaport.requestSeawayEntrance(s);
            synchronized(out) {System.out.print(s.id + " entered the seaway.\n");}
            s.setAssignedDock(seaport.requestPortEntrance(s));
            synchronized(out) {System.out.print(s.id + " is about to enter the port.\n");}
            seaport.signalPortEntered(s);
            synchronized(out) {System.out.print(s.id + " left the seaway and entered the port.\n");}
            seaport.requestPortExit(s);
            synchronized(out) {System.out.print(s.id + " is about to leave the port.\n");}
            seaport.signalPortExited(s);
            synchronized(out) {System.out.print(s.id + " left the port and entered the seaway.\n");}
            seaport.signalShipSailedAway(s);
            synchronized(out) {System.out.print(s.id + " left the seaway.\n");}
        }
    }

    static Object out = new Object();

    public static void shipTest() {
        System.out.println("-----SHIPTEST-----");
        SeaportManagerImpl seaport = new SeaportManagerImpl();
        seaport.init(10, 5);
        Ship s = new Ship(1, 0);
        seaport.requestSeawayEntrance(s);
        synchronized (out) {
            System.out.print(s.id + " entered the seaway.\n");
        }
        s.setAssignedDock(seaport.requestPortEntrance(s));
        synchronized (out) {
            System.out.print(s.id + " is about to enter the port.\n");
        }
        seaport.signalPortEntered(s);
        synchronized (out) {
            System.out.print(s.id + " left the seaway and entered the port.\n");
        }
        seaport.requestPortExit(s);
        synchronized (out) {
            System.out.print(s.id + " is about to leave the port.\n");
        }
        seaport.signalPortExited(s);
        synchronized (out) {
            System.out.print(s.id + " left the port and entered the seaway.\n");
        }
        seaport.signalShipSailedAway(s);
        synchronized (out) {
            System.out.print(s.id + " left the seaway.\n");
        }
    }

    public static void threadTest(){
        System.out.println("-----THREADTEST-----");
        SeaportManagerImpl seaport = new SeaportManagerImpl();
        seaport.init(10, 5);
        int amountOfShips = 20;
        Ship[] ships = new Ship[amountOfShips];
        Thread[] thread = new Thread[amountOfShips];
        for(int i=0; i<amountOfShips; ++i){
            ships[i] = new Ship(i%10+1, i);
            MyThread myThread = new MyThread(ships[i], seaport);
            thread[i] = new Thread(myThread);
        } for(int i = 0; i<amountOfShips; ++i) {
            thread[i].start();
        }
    }

    public static void main(String[] args) {
        shipTest();
        threadTest();
    }
}

// class SeaportManagerImpl{

//     private Semaphore OpenDocks;

//     private Semaphore Seaway;
//     private Semaphore arrayUsage;

//     private Ship docksTaken[];
//     private int docksize;

//     public void init(int numberOfDocks, int seawayCapacity)
//     {
//         docksTaken = new Ship[numberOfDocks];
//         docksize = numberOfDocks;
//         arrayUsage = new Semaphore( 1);
//         Seaway = new Semaphore( seawayCapacity, true );
//         OpenDocks = new Semaphore( 1);
//     }

//     public void requestSeawayEntrance (Ship s)
//     {
//         try {
//             OpenDocks.acquire();
//         } catch (InterruptedException e1) {}

//         try {
//             Seaway.acquire();
//         } catch (InterruptedException e) {}
        
//         while (!insertShip(s))
//         {

//         }
//         OpenDocks.release();
//     }

//     public int requestPortEntrance(Ship s)
//     {

//         try {
//             OpenDocks.acquire();
//         }
//         catch ( InterruptedException e ) {};
//         try {
//             Seaway.acquire();
//         }
//         catch ( InterruptedException e ) {};

//         while (!insertShip(s));
//         OpenDocks.release();

//         return s.getAssignedDock();
//     }

//     public void signalPortEntered(Ship s)
//     {
//         Seaway.release();

//     }

//     public void requestPortExit(Ship s)
//     {
//         try {
//         Seaway.acquire();
//         } catch (InterruptedException e) {}
//     }

//     public void signalPortExited(Ship s)
//     {
//         try {
//             arrayUsage.acquire();
//         } catch (InterruptedException e) {}

//         int currentI = s.getAssignedDock();
//         for (int i = currentI; i < currentI + s.getDockingSize(); i++)
//         {
//             docksTaken[i] = null;
//         }

//         arrayUsage.release();
    
//     }

//     public void signalShipSailedAway(Ship s)
//     {
//         Seaway.release();
//     }

//     public boolean insertShip(Ship s)
//     {
//         boolean inserted = false;
//         int currentI = 0;
//         int currentLen = 0;

//         try {
//             arrayUsage.acquire();
//         } catch (InterruptedException e) {}


//         for (int i = 0; i < docksize; i++)
//         {
//             if (docksTaken[i] == null)
//             {
//                 currentLen++;
//                 if (currentLen == s.getDockingSize())
//                 {
//                     inserted = true;
//                     break;
//                 }
//             }
//             else
//             {
//                 currentLen = 0;
//                 currentI = i + 1;
//             }
//         }

//         if (inserted)
//         {
//             for (int i = currentI; i < s.getDockingSize() + currentI; i++)
//             {
//                 docksTaken[i] = s;
//             }
//         }

//         arrayUsage.release();

//         return inserted;
//     }
// }


