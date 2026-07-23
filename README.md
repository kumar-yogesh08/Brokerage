# 📈 Brokerage & Net P&L Calculator

A lightweight, portable Windows desktop application designed to accurately calculate Net Profit & Loss, comprehensive brokerage charges, and break-even points for your stock market trades. 

Currently supports **Groww** and **Zerodha** fee structures.

---

## ✨ Features

* **No Installation Required:** Completely portable `.exe`. Just download and run.
* **Dual Broker Support:** Toggle instantly between Groww and Zerodha charge structures.
* **Single Trade Mode:** 
  * Calculate turnover, gross P&L, total charges (Brokerage, STT, Exchange Fees, GST, SEBI, Stamp Duty), and Net P&L.
  * Instant Break-Even price calculation.
  * Maximum quantity calculator based on your available investment capital.
* **Multi-Trade Mode:** 
  * Add multiple trades (mix of Delivery and Intraday) to a running ledger.
  * View total aggregated turnover, gross P&L, total charges, and Net P&L for the day.
* **Modern UI:** Built with a sleek, distraction-free dark mode interface.

---

## 🚀 How to Download and Run

Since this is a standalone executable, you do not need Python or any other dependencies installed on your system.

1. **Download:** To directly download the application, click **[Download Brokerage.exe](https://github.com/kumar-yogesh08/Brokerage/releases/download/v1.0.0/Brokerage.exe)**, or visit the [Releases](https://github.com/kumar-yogesh08/Brokerage/releases/latest) page.
2. **Run:** Double-click the downloaded executable to open the calculator.
3. **Optional:** You can move this `.exe` to your Desktop or pin it to your Taskbar for quick access during trading hours.

### ⚠️ A Note on Windows SmartScreen
Because this application is packaged as an independent executable without an expensive corporate publisher certificate, **Windows Defender SmartScreen** may flag it as an "unrecognized app" the first time you open it. 
* To run it, simply click **"More info"** and then **"Run anyway"**.
---

## 📸 Screenshots

### Single Trade Mode
Get an instant, detailed breakdown of a single transaction. This view provides your Gross P&L, Total Charges, and exact Net P&L. It also features a capital allocation tool to determine the maximum shares you can buy based on your investment amount, alongside an automatic Break-Even price calculator.

<img width="768" height="406" alt="Brokerage_First_SS" src="https://github.com/user-attachments/assets/4fec437a-23dc-4620-9cc2-e620b01b192b" />

### Multi-Trade Mode
Perfect for active trading sessions. Add multiple Equity Delivery or Intraday trades to your ledger to calculate your total aggregated Turnover, Gross P&L, combined Charges, and final Net P&L across all positions for the day.

<img width="766" height="596" alt="Brokerage_Second_SS" src="https://github.com/user-attachments/assets/2417e0e1-fd1c-4e99-be6a-650d71c0e66e" />

---

## ⚖️ Disclaimer

This tool is for educational and informational purposes only. While the mathematical formulas are strictly mapped to the publicly available fee structures of the supported brokers, actual platform charges may occasionally vary due to micro-rounding differences or sudden regulatory changes. Always verify final charges on your broker's official contract note.
