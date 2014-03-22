#!/bin/bash
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 1 0 model sys >accfile.1_0
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 2 0 model sys >accfile.2_0
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 4 0 model sys >accfile.4_0
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 10 0 model sys >accfile.10_0
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 20 0 model sys >accfile.20_0
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 50 0 model sys >accfile.50_0

./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 1 0.1 model sys >accfile.1_01
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 2 0.1 model sys >accfile.2_01
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 4 0.1 model sys >accfile.4_01
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 10 0.1 model sys >accfile.10_01
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 20 0.1 model sys >accfile.20_01
./build_dt.sh ../../dropbox/09-10/572/hw2/examples/train.vectors.txt ../../dropbox/09-10/572/hw2/examples/test.vectors.txt 50 0.1 model sys >accfile.50_01

