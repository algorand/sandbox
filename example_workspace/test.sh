# see https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/#creating-the-smart-contract
goal app create \
    --creator QGB43KZO6H32VRXRJ52IF7USO5JWBINQZ764CWZGZAQ7NW3UQWJWZYY2FI  \
    --approval-prog test.teal \
    --clear-prog test.teal \
    --global-byteslices 0 \
    --global-ints 0 \
    --local-byteslices 0 \
    --local-ints 0 \
    --extra-pages 0 \
    --dryrun-dump \
    --out=dumptx.dr

tealdbg debug test.teal --dryrun-req dumptx.dr --listen 0.0.0.0