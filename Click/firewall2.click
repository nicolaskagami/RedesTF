// You can run it at user level (as root) as
// 'userlevel/click < conf/Print-pings.click'
// or in the kernel with
// 'click-install conf/Print-pings.click'

define($DEV h2)

FromDevice($DEV-eth0, SNIFFER false, PROMISC true, BURST 8)	// read packets from device
   -> pkt :: Classifier(12/0800, -)
   -> ck :: CheckIPHeader(OFFSET 14)
   -> IPFilter(
		drop all)
   -> queue :: ThreadSafeQueue(10000)
   pkt[1] -> queue
   ck[1] -> queue
   -> ToDevice($DEV-eth1, BURST 8);

FromDevice($DEV-eth1, SNIFFER false, PROMISC true, BURST 8 )	// read packets from device
   -> pkt1 :: Classifier(12/0800, -)
   -> ck1 :: CheckIPHeader(OFFSET 14)
   -> IPFilter(  
		drop all)
   -> queue1 :: ThreadSafeQueue(10000)
   pkt1[1] -> queue1
   ck1[1] -> queue1
   -> ToDevice($DEV-eth0, BURST 8);
