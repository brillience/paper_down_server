#!/bin/bash
/home/zxb/workspace/paper_down_server/venv/bin/python /home/zxb/workspace/paper_down_server/wos_crawl/runSpider.py > wos_crawl.log
/home/zxb/workspace/paper_down_server/venv/bin/python /home/zxb/workspace/paper_down_server/wos_crawl/wos_crawl/push_pdf_to_path.py
