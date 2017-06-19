# Graphene-Witness-Monitor
Script to monitor the health of Graphene Witnesses and Seed node

Thanks to @RoelandP and @Xeroc for their prior work in this tool and supporting libraries.


##  Preface
This script is in ALPHA and has only been tested with the Peerplays network although should work with other Graphene based chains. This script is in testing and i highly recommend you do not activate the HotSwitch function until it has been fully tested.

Using this script for monitoring should not cause any harm but still should considered ALPHA

If you cannot help yourself and activate the HotSwitch function, it should only be ran on a machine that you have full control of. Do not store ACTIVE keys for your witnesses on 3rd party VPS providers.


## Installation 
* Install [Python-Graphene](https://github.com/xeroc/python-graphenelib)
* Copy witnesshealth.py to location on disk (script requires access to GrapheneAPI)

## Start Monitor
The monitor connects to the CLI wallet RPC interface; for monitoring the wallet can be locked. If you use the HotSwitch feature you will need to have you wallet unlocked to be able to sign and broadcase the witness_update transaction

### Start Cli Wallet
```
./cli_wallet -r 127.0.0.1:8092
```

### Start monitor in a new terminal
```
python3 witnesshealth.py  
```

# IMPORTANT NOTE

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
