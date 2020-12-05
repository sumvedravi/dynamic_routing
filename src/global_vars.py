hosts = [] 	#format	[host1 mac, host2 mac, ...] 
devices = [] 	#format [dev1 id, dev2 id, ...]
links = [] 	#format [(src device , src port (int), dst device, dst port (int)), ...]
link_stats = {} #format {
			 #'src_device-dst_device': { calculated_bw_being_used, number_of_flows, current_link_delay},
			 #'src_device-dst_device': { calculated_bw_being_used, number_of_flows, current_link_delay},

		#}
flow_paths = {}			
graph = nx.Graph()


#all_shortest_paths() = if multiple paths are of equal length then give all those paths back

#shortest_path = gives top shortest


#init_flow_paths_var();

'''
flow_paths = { 
	        'src_host-dst_host': {
			active: True/False
			path_index: index_value_of_shortest_path
			paths: [ path1=(dev_a, dev_b, ... ), path2=() ] #these are shortest paths available
			path_values: [ path1_val, path2_val, ... ]  # calculated path efficency values 
			flowId: [(deviceID, flowID), (deviceID2, flowID), ... ] #for the selected path (from path_index) keep a list of all device + flowID pairs
		
		},
		
	        'src_host-dst_host': {
			active: True/False
			path_index: index_value_of_shortest_path
			paths: [ path1=(dev_a, dev_b, ... ), path2=() ] #these are shortest paths available
			path_values: [ path1_val, path2_val, ... ]  # calculated path efficency values 
			flowId: [(deviceID, flowID), (deviceID2, flowID), ... ] #for the selected path (from path_index) keep a list of all device + flowID pairs
		
		}
}

	1. use: link_monitor 
		if changes -> update graph + update paths through calc_route
	2. use: portstat_monitor
		update link_stats bw values, number of flows, realtime link delays
	3. use: flow_monitor
		local variable => tracked_flow_ids  # iperf h1 h2 --> new TCP connection is online
		check for new flow -> if new flow exists then make flow active and add flowId's to flow_paths
		calc_shortest_paths
	4. use: routing_engine:
		calc route efficency values using link_stats and paths in flow_paths per connection
		select new path per active flow
			-> delete existing flows (using FlowIds in flow_paths)
			-> add new flows
			-> update FlowIds, in flow_paths
		
	Link	
	DevA -> DevB

	path is full distance
	Src->A->B->D->Target

	Link Efficency = (Link_max_bandwidth - Sum(all flows on link)]/num_flows 
	Path Efficency = Link_delays_normalized to [0-1] + Sum(Link Efficencies values in path normalized to [0-1])
	
'''
