{
    "FlowLogs": [
        {
            "LogDestinationType": "cloud-watch-logs", 
            "Tags": [
                {
                    "Value": "polystudent", 
                    "Key": "Environment"
                }, 
                {
                    "Value": "vpc-flow-logs-rejected", 
                    "Key": "Name"
                }
            ], 
            "ResourceId": "vpc-04514fbb457dca0dc", 
            "CreationTime": "2025-11-15T06:40:39.929Z", 
            "LogGroupName": "VPC-Flow-Logs-Rejected", 
            "TrafficType": "REJECT", 
            "FlowLogStatus": "ACTIVE", 
            "LogFormat": "${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status}", 
            "FlowLogId": "fl-0387b4279e0829b39", 
            "MaxAggregationInterval": 60, 
            "DeliverLogsPermissionArn": "arn:aws:iam::983201656846:role/VPCFlowLogsToCloudWatch", 
            "DeliverLogsStatus": "SUCCESS"
        }
    ]
}
2025-10-24 19:50:09         93 vpcflow/demo-flow.txt
