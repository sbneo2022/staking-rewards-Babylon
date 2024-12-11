
## Prerequisites

- Python 3.x
- Streamlit
- Pandas

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:sbneo2022/stak-rew.git
   cd stak-rew
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure your `requirements.txt` includes `streamlit` and `pandas`.

## Usage

### Running the App

To run the Streamlit app, use the following command:

```bash
make run
```

This will start the Streamlit server and open the app in your default web browser.

### Accessing the App on Your Phone

To access the app on your phone:

1. Ensure your phone is connected to the same network as your computer.
2. Find your computer's local IP address.
3. Open a web browser on your phone and enter the URL: `http://<your-local-ip>:8501`

### Help

For a list of available Makefile commands, use:

```bash
make help
```

## File Structure

- `cryptometric_dashboard.py`: The main Streamlit app file.
- `Makefile`: Contains commands to run the app and display help.
- `offline_data/`: Directory containing CSV files with staking and price data.

