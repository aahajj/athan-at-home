# Athan @ Home

If you live in a place where you cannot hear the athan, you’re probably relying on an app (such as Mawaqit) on your phone to know the prayer times. While these apps generally work well, I’ve had an issue with not being able to hear my phone when the athan goes off for Fajr.

I tried using another device, such as my iPad, where I don’t enable DND mode at night. However, the athan often doesn’t play fully. Setting an alarm was a temporary solution, but it is static and not ideal long-term.

I realized I don’t just want to hear the athan from my phone—I want a source that plays it louder and clearer. At first, I considered buying a smart home speaker, but since I don’t want a device that’s always listening, I decided to build my own solution.



## Requirements

1. Raspberry Pi (or any similar device)
2. Speakers
3. Git, Python3, and pip3 installed



## How It Works

* The Python script fetches the **monthly prayer calendar** from Mawaqit once per month.
* Daily prayer times are read from a local `calendar.json` file, reducing network dependency.
* Athan is played automatically at scheduled times from a **local audio file**.
* Logs are written to `out/athan.log` for easy monitoring.
* The app can be started/stopped using the provided **Bash script**, which also activates the Python virtual environment.



## Installation

Clone the repository and set up the Python environment:

```bash
git clone https://github.com/aahajj/athan-home.git
cd athan-home
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt
```

The project includes a Bash script `athan.sh` to start or stop the app. Make it executable first:

```bash
cd src
chmod +x athan.sh
```

* Start Athan (activates the Python environment, runs in the background):

```bash
./athan.sh a
```

* Stop Athan (deactivates and kills the process):

```bash
./athan.sh d
```

> Logs are saved in `out/athan.log`. The monthly calendar is stored in `out/calendar.json`.

