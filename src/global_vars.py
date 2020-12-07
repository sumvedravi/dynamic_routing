import networkx as nx


hosts = [] 	#format	[host1 mac, host2 mac, ...] 
devices = [] 	#format [dev1 id, dev2 id, ...]

links = {}	#format {src_dev: 
			 #{
			    #dst_dev:{
				#con_type = 'h-s' , 's-s', 's-h'
				#status: '1 (for up) or 0 (for down)
				#max_bw: val
				#bw: realtime values
				#link_flow_count: val
				#delay: realtime values
				#delay_norm: normailzed delay value
				#bw_norm: normalized bw value
				#efficency: val

				#src_port: src device port 
				#dst_port: dst device port
			    #}, 
			    #dst_dev2:{..} 
			 #}
			#},
			#src_dev2:{}
		#}
flow_paths = {}			
graph = nx.Graph()


#all_shortest_paths() = if multiple paths are of equal length then give all those paths back
#shortest_path = gives top shortest
#init_flow_paths_var();
#links = [] 	#format {src_dev: {dst_dev:{src_port: port_in, dst_port: port_out }, dst_dev2:{} }}
		#old - format [src device , src port (int), dst device, dst port (int)), ...]
#link_stats = {} #format {
			 #'src_device-dst_device': { calculated_bw_being_used, number_of_flows, current_link_delay},
			 #'src_device-dst_device': { calculated_bw_being_used, number_of_flows, current_link_delay},

'''
flow_paths = { 
	        'src_mac': {
			'dst_mac': {
<<<<<<< HEAD
			packets: 						# number of packets gone through the flow
			last_changed: 						# number of program iterations since packets value has changed (sum over all flows) 
			path: [ path1=(dev_a, dev_b, ... ), path2=() ] 		# shortest path available
			path_efficency: val 					# calculated path efficency value  
			flow_ids: {deviceID: { flow_id: flowID,
					     packets: num_pkts 
					     last_changed: val }} 		# for the selected path (from path_index) keep a list of all devices and flow data			},

			'dst_mac': {
			packets: 						# number of packets gone through the flow
			last_changed: 						# number of program iterations since packets value has changed (sum over all flows)
			path: [ path1=(dev_a, dev_b, ... ), path2=() ] 		# shortest path available
			path_efficency: val 					# calculated path efficency value  
			flow_ids: {deviceID: { flow_id: flowID,
					     packets: num_pkts 
					     last_changed: val }} 		# for the selected path (from path_index) keep a list of all devices and flow data
=======
			active: True/False
			path_index: index_value_of_shortest_path
			paths: [ path1=(dev_a, dev_b, ... ), path2=() ] #these are shortest paths available
			path_values: [ path1_val, path2_val, ... ]  # calculated path efficency values 
			flowId: [(deviceID, flowID), (deviceID2, flowID), ... ] #for the selected path (from path_index) keep a list of all device + flowID pairs
		
			},
			'dst_mac': {
			active: True/False
			path_index: index_value_of_shortest_path
			paths: [ path1=(dev_a, dev_b, ... ), path2=() ] #these are shortest paths available
			path_values: [ path1_val, path2_val, ... ]  # calculated path efficency values 
			flowId: [(deviceID, flowID), (deviceID2, flowID), ... ] #for the selected path (from path_index) keep a list of all device + flowID pairs
		
>>>>>>> 9d43d81aa6209f0b8adad2fb0947ca8494725bd0
			}	
		 },
		
	        'src2_mac: {
			'dst_mac': {
<<<<<<< HEAD
			packets: 						# number of packets gone through the flow
			last_changed: 						# number of program iterations since packets value has changed (sum over all flows)
			path: [ path1=(dev_a, dev_b, ... ), path2=() ] 		# shortest path available
			path_efficency: val 					# calculated path efficency value  
			flow_ids: {deviceID: { flow_id: flowID,
					     packets: num_pkts 
					     last_changed: val }} 		# for the selected path (from path_index) keep a list of all devices and flow data			},
=======
			active: True/False
			path_index: index_value_of_shortest_path
			paths: [ path1=(dev_a, dev_b, ... ), path2=() ] #these are shortest paths available
			path_values: [ path1_val, path2_val, ... ]  # calculated path efficency values 
			flowId: [(deviceID, flowID), (deviceID2, flowID), ... ] #for the selected path (from path_index) keep a list of all device + flowID pairs
		
			},
>>>>>>> 9d43d81aa6209f0b8adad2fb0947ca8494725bd0
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
