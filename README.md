Search INDX on NTFS
===================
This programm searches INDX artefacts on (broken completely) NTFS partition.


External dependencies
===================

https://tzworks.net/download_links.php

Windows INDX Slack Parser (wisp)
(this project was tested with wisp32.v.0.20.lin.tar.gz)
You have to extract content of this archive into '3rdparty' subfolder.


How to use
===================

> $ make search_INDX

> $ ./search_INDX <NTFS_disk_image> > indx_list.txt

> $ ./parse_INDX_tree.py  <NTFS_disk_image> indx_list.txt

