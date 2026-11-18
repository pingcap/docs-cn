"""Write the configuration for the media upload's COSCLI invocation."""

import json
import os


config = {
    "cos": {
        "base": {
            "disableencryption": "true",
            "mode": "SecretKey",
            "protocol": "https",
            "secretid": os.environ["TENCENTCLOUD_SECRET_ID"],
            "secretkey": os.environ["TENCENTCLOUD_SECRET_KEY"],
        }
    }
}
config_path = os.environ["COSCLI_CONFIG"]
with open(config_path, "w", encoding="utf-8") as config_file:
    json.dump(config, config_file)
os.chmod(config_path, 0o600)
