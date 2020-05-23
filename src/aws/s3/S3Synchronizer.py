from __future__ import absolute_import

import logging
import os
import subprocess
import threading
import time

logger = logging

class CheckpointSynchronizer():
    """Placeholder docstring"""

    def __init__(self, checkpoint_local_dir, checkpoint_s3_uri):
        """Initialize ``CheckpointSynchronizer`` instance.
        Args:            
            checkpoint_local_dir (str): Directory for logs to be sent to S3
            checkpoint_s3_uri (str): S3 directory to be synchronized
            
        """
        
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.event = threading.Event()
        self.checkpoint_local_dir = checkpoint_local_dir
        self.checkpoint_s3_uri = checkpoint_s3_uri
    
    def stop(self):
        self.event.set()
    
    def run_async(self):
        self.thread.start()

    def run(self):
        logger.info(f"S3 checkpoint synchronizer started")
        args = ["aws", "s3", "sync", self.checkpoint_local_dir, self.checkpoint_s3_uri]                        
        while not self.event.is_set():
            subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)                
            print(f"{self.checkpoint_local_dir} synced to {self.checkpoint_s3_uri}")
            self.event.wait(10)
        subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
