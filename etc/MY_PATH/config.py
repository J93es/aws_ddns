aws_ddns_config = {
    "USE_DISCORD" : True,
    "DISCORD_WEB_HOOK_URI" : "CUSTOM_WEB_HOOK_URI",
    "AWS_ACCESS_KEY_ID" : "CLIENT_PUBLIC_KEY",
    "AWS_SECRET_ACCESS_KEY" : "CLIENT_SECRET_KEY",
    "QUIET_MODE": False,
    
    "hostedZones": { 
        
        "example1.com" : {
            "records" : {
                "example1.com" : {
                    "TTL": 300
                },
                "www.example1.com" : {
                    "TTL": 200
                },
            },
           #"Comment" : ""
        },
        
        "example2.net" : {
            "records" : {
                "example2.net" : {
                    "TTL": 300
                },
            },
           "Comment" : ""
        },
    },
}
