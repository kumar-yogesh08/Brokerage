import customtkinter as ctk
import ctypes

# ==========================================
# CORE MATH ENGINE
# ==========================================
def get_trade_metrics(qty, buy_price, sell_price, trade_type, broker):
    buy_value = buy_price * qty
    sell_value = sell_price * qty
    turnover = buy_value + sell_value
    gross_pl = sell_value - buy_value

    if broker == "Zerodha":
        if trade_type == "Equity Delivery":
            brokerage_buy = 0.0
            brokerage_sell = 0.0
        else:
            brokerage_buy = min(20.0, 0.0003 * buy_value)
            brokerage_sell = min(20.0, 0.0003 * sell_value)
    else:
        brokerage_buy = min(20.0, 0.001 * buy_value)
        brokerage_sell = min(20.0, 0.001 * sell_value)

    brokerage_charges = round(brokerage_buy + brokerage_sell, 2)
    exchange_charges = round(0.0000297 * turnover, 2)
    sebi_fees = round(0.000001 * turnover, 2)

    if trade_type == "Equity Delivery":
        stt = round(0.001 * turnover)
        stamp_duty = round(0.00015 * buy_value)
    else: 
        stt = round(0.00025 * sell_value)
        stamp_duty = round(0.00003 * buy_value)

    gst = round(0.18 * (brokerage_charges + exchange_charges + sebi_fees), 2)
    total_charges = brokerage_charges + stt + exchange_charges + sebi_fees + gst + stamp_duty
    net_pl = gross_pl - total_charges
    
    return turnover, gross_pl, total_charges, net_pl

def get_pl_for_sell(qty, buy_price, sell_price, trade_type, broker):
    _, _, _, net_pl = get_trade_metrics(qty, buy_price, sell_price, trade_type, broker)
    return net_pl

# ==========================================
# UI SETUP & THEME
# ==========================================
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("brokerage Calc")
root.attributes("-topmost", True)

try:
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    value = ctypes.c_int(2)
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
except Exception: pass 

BG_COLOR = "#121212"
INPUT_BG = "#162822" 
INPUT_FG = "#00d09c" 
LABEL_COLOR = "#a1a1a1"
BORDER_COLOR = "#2a2a2a"

root.configure(fg_color=BG_COLOR)

entry_kwargs = {
    "fg_color": INPUT_BG, "text_color": INPUT_FG, "border_color": BORDER_COLOR, 
    "corner_radius": 6, "border_width": 1, "font": ("Segoe UI", 12, "bold"), "height": 26
}
bold_font = ("Segoe UI", 12, "bold")

# Variables
broker_var = ctk.StringVar(value="Groww")
mode_var = ctk.StringVar(value="Single Trade")

type_var = ctk.StringVar(value="Equity Delivery")
qty_var = ctk.StringVar(value="28")
buy_var = ctk.StringVar(value="714")
sell_var = ctk.StringVar(value="730")
invest_var = ctk.StringVar(value="40000")
invest_buy_var = ctk.StringVar(value="714")

multi_type_var = ctk.StringVar(value="Equity Intraday")
multi_qty_var = ctk.StringVar(value="")
multi_buy_var = ctk.StringVar(value="")
multi_sell_var = ctk.StringVar(value="")
multi_trades_list = [] 

# ==========================================
# LOGIC CONTROLLERS
# ==========================================
def calculate_single(*args):
    try:
        qty = float(qty_var.get())
        buy_price = float(buy_var.get())
        sell_price = float(sell_var.get())
        trade_type = type_var.get()
        broker = broker_var.get()
    except ValueError: return 

    turnover, gross_pl, total_charges, net_pl = get_trade_metrics(qty, buy_price, sell_price, trade_type, broker)

    lbl_turnover_val.configure(text=f"₹{turnover:,.2f}")
    lbl_gross_val.configure(text=f"₹{gross_pl:,.2f}")
    lbl_charges_val.configure(text=f"₹{total_charges:,.2f}")
    lbl_net_val.configure(text=f"₹{net_pl:,.2f}", text_color="#00d09c" if net_pl >= 0 else "#eb5b3c")

    if qty > 0 and buy_price > 0:
        low_sell, high_sell, best_sell = buy_price, buy_price * 2.0, buy_price
        for _ in range(50):
            mid_sell = (low_sell + high_sell) / 2
            if get_pl_for_sell(qty, buy_price, mid_sell, trade_type, broker) < 0: low_sell = mid_sell 
            else: high_sell, best_sell = mid_sell, mid_sell
        lbl_breakeven_val.configure(text=f"₹{best_sell:,.2f}")
    else: lbl_breakeven_val.configure(text="₹0.00")

def calculate_max_qty(*args):
    try:
        investment = float(invest_var.get())
        buy_p = float(invest_buy_var.get())
        lbl_max_qty_val.configure(text=f"{int(investment // buy_p)} shares" if buy_p > 0 else "0 shares")
    except ValueError: lbl_max_qty_val.configure(text="--")

def update_multi_ui(*args):
    for widget in scrollable_trades_frame.winfo_children(): widget.destroy()
    total_turnover = total_gross = total_charges = total_net = 0.0
    broker = broker_var.get()

    for trade in multi_trades_list:
        t_turn, t_gross, t_chg, t_net = get_trade_metrics(trade['q'], trade['b'], trade['s'], trade['t'], broker)
        total_turnover += t_turn; total_gross += t_gross; total_charges += t_chg; total_net += t_net
        
        row = ctk.CTkFrame(scrollable_trades_frame, fg_color="#1a1a1a", corner_radius=6)
        row.pack(fill="x", pady=2, padx=5)
        
        color = "#00d09c" if t_net >= 0 else "#eb5b3c"
        ctk.CTkLabel(row, text=f"[{trade['t'][:2].upper()}] Q: {trade['q']} | B: ₹{trade['b']} | S: ₹{trade['s']}", font=("Segoe UI", 11), text_color=LABEL_COLOR).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(row, text=f"₹{t_net:,.2f}", font=bold_font, text_color=color).pack(side="right", padx=10)

    lbl_m_turnover.configure(text=f"₹{total_turnover:,.2f}")
    lbl_m_gross.configure(text=f"₹{total_gross:,.2f}")
    lbl_m_charges.configure(text=f"₹{total_charges:,.2f}")
    lbl_m_net.configure(text=f"₹{total_net:,.2f}", text_color="#00d09c" if total_net >= 0 else "#eb5b3c")

def add_multi_trade():
    try:
        q, b, s, t = float(multi_qty_var.get()), float(multi_buy_var.get()), float(multi_sell_var.get()), multi_type_var.get()
        multi_trades_list.append({'q': q, 'b': b, 's': s, 't': t})
        multi_qty_var.set(""); multi_buy_var.set(""); multi_sell_var.set("")
        update_multi_ui()
    except ValueError: pass

def switch_mode(*args):
    if mode_var.get() == "Single Trade":
        frame_multi_mode.pack_forget()
        frame_single_mode.pack(fill="both", expand=True, padx=10, pady=0)
        root.geometry("620x300")
        root.minsize(620, 300)
        root.maxsize(620, 300)
    else:
        frame_single_mode.pack_forget()
        frame_multi_mode.pack(fill="both", expand=True, padx=10, pady=0)
        root.geometry("620x450")
        root.minsize(620, 450)
        root.maxsize(620, 450)

for var in (qty_var, buy_var, sell_var, type_var, broker_var): var.trace_add("write", calculate_single)
for var in (invest_var, invest_buy_var): var.trace_add("write", calculate_max_qty)
broker_var.trace_add("write", update_multi_ui)

# ==========================================
# TOP BAR (ALWAYS VISIBLE)
# ==========================================
top_bar = ctk.CTkFrame(root, fg_color="transparent")
top_bar.pack(fill="x", padx=15, pady=(10, 10))

ctk.CTkSegmentedButton(
    top_bar, variable=broker_var, values=["Groww", "Zerodha"],
    font=("Segoe UI", 12, "bold"), height=26, width=160,
    selected_color="#00d09c", selected_hover_color="#00a87e",
    unselected_color=INPUT_BG, unselected_hover_color="#1c3b31"
).pack(side="left")

ctk.CTkSegmentedButton(
    top_bar, variable=mode_var, values=["Single Trade", "Multi Trade"], command=switch_mode,
    font=("Segoe UI", 12, "bold"), height=26, width=200,
    selected_color="#2a2a2a", selected_hover_color="#333333",
    unselected_color="#121212", unselected_hover_color="#1a1a1a"
).pack(side="right")

# ==========================================
# SINGLE MODE FRAME
# ==========================================
frame_single_mode = ctk.CTkFrame(root, fg_color="transparent")

main_frame = ctk.CTkFrame(frame_single_mode, fg_color="transparent")
main_frame.pack(fill="x", pady=0)

frame_inputs = ctk.CTkFrame(main_frame, fg_color="transparent")
frame_inputs.pack(side="left")

ctk.CTkLabel(frame_inputs, text="Type:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=2, padx=(0,2))
ctk.CTkOptionMenu(
    frame_inputs, variable=type_var, values=["Equity Delivery", "Equity Intraday"],
    fg_color=INPUT_BG, text_color=INPUT_FG, button_color=INPUT_BG, button_hover_color="#1c3b31", 
    corner_radius=6, font=("Segoe UI", 12, "bold"), width=135, height=26, dropdown_fg_color=BG_COLOR, dropdown_text_color=INPUT_FG
).grid(row=0, column=1, pady=2, padx=(0, 8))

ctk.CTkLabel(frame_inputs, text="Buy:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=0, column=2, sticky="e", pady=2, padx=(0,2))
ctk.CTkEntry(frame_inputs, textvariable=buy_var, width=70, **entry_kwargs).grid(row=0, column=3, pady=2)

ctk.CTkLabel(frame_inputs, text="Qty:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", pady=2, padx=(0,2))
ctk.CTkEntry(frame_inputs, textvariable=qty_var, width=135, **entry_kwargs).grid(row=1, column=1, pady=2, padx=(0, 8))

ctk.CTkLabel(frame_inputs, text="Sell:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=1, column=2, sticky="e", pady=2, padx=(0,2))
ctk.CTkEntry(frame_inputs, textvariable=sell_var, width=70, **entry_kwargs).grid(row=1, column=3, pady=2)

ctk.CTkFrame(main_frame, width=1, fg_color="#333333").pack(side="left", fill="y", padx=8, pady=2) 

frame_breakdown = ctk.CTkFrame(main_frame, fg_color="transparent")
frame_breakdown.pack(side="left")

for i, text in enumerate(["Turnover:", "Gross P&L:", "Charges:"]):
    ctk.CTkLabel(frame_breakdown, text=text, text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=i, column=0, sticky="w", pady=0)

lbl_turnover_val = ctk.CTkLabel(frame_breakdown, text="₹0.00", font=bold_font, text_color="white")
lbl_turnover_val.grid(row=0, column=1, sticky="e", padx=(8,0))
lbl_gross_val = ctk.CTkLabel(frame_breakdown, text="₹0.00", font=bold_font, text_color="white")
lbl_gross_val.grid(row=1, column=1, sticky="e", padx=(8,0))
lbl_charges_val = ctk.CTkLabel(frame_breakdown, text="₹0.00", font=bold_font, text_color="white")
lbl_charges_val.grid(row=2, column=1, sticky="e", padx=(8,0))

ctk.CTkFrame(main_frame, width=1, fg_color="#333333").pack(side="left", fill="y", padx=8, pady=2) 

frame_net = ctk.CTkFrame(main_frame, fg_color="transparent")
frame_net.pack(side="left", padx=0)
ctk.CTkLabel(frame_net, text="Net P&L", font=("Segoe UI", 12), text_color="white").pack(anchor="center", pady=(2,0))
lbl_net_val = ctk.CTkLabel(frame_net, text="₹0.00", font=("Segoe UI", 24, "bold"))
lbl_net_val.pack(anchor="center", pady=0)

bottom_frame = ctk.CTkFrame(frame_single_mode, fg_color="transparent")
bottom_frame.pack(fill="x", pady=(15, 0))

frame_max_qty = ctk.CTkFrame(bottom_frame, fg_color="transparent")
frame_max_qty.pack(side="left")

ctk.CTkLabel(frame_max_qty, text="Inv:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=(0,2))
ctk.CTkEntry(frame_max_qty, textvariable=invest_var, width=65, **entry_kwargs).grid(row=0, column=1, padx=(0,8))
ctk.CTkLabel(frame_max_qty, text="Buy:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=0, column=2, sticky="w", padx=(0,2))
ctk.CTkEntry(frame_max_qty, textvariable=invest_buy_var, width=60, **entry_kwargs).grid(row=0, column=3, padx=(0,8))
ctk.CTkLabel(frame_max_qty, text="Max Qty:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).grid(row=0, column=4, sticky="w", padx=(0,2))
lbl_max_qty_val = ctk.CTkLabel(frame_max_qty, text="0 shares", font=bold_font, text_color="white")
lbl_max_qty_val.grid(row=0, column=5, sticky="w")

ctk.CTkFrame(bottom_frame, width=1, fg_color="#333333").pack(side="left", fill="y", padx=10) 
frame_breakeven = ctk.CTkFrame(bottom_frame, fg_color="transparent")
frame_breakeven.pack(side="left") 
ctk.CTkLabel(frame_breakeven, text="Break-Even:", text_color=LABEL_COLOR, font=("Segoe UI", 12)).pack(side="left", padx=(0,4))
lbl_breakeven_val = ctk.CTkLabel(frame_breakeven, text="₹0.00", font=("Segoe UI", 14, "bold"), text_color="#f0b90b") 
lbl_breakeven_val.pack(side="left")

# ==========================================
# MULTI MODE FRAME
# ==========================================
frame_multi_mode = ctk.CTkFrame(root, fg_color="transparent")

multi_input_row = ctk.CTkFrame(frame_multi_mode, fg_color="transparent")
multi_input_row.pack(fill="x", pady=(0, 10))

ctk.CTkOptionMenu(
    multi_input_row, variable=multi_type_var, values=["Equity Intraday", "Equity Delivery"],
    fg_color=INPUT_BG, text_color=INPUT_FG, button_color=INPUT_BG, button_hover_color="#1c3b31", 
    corner_radius=6, font=("Segoe UI", 12, "bold"), width=120, height=26, dropdown_fg_color=BG_COLOR, dropdown_text_color=INPUT_FG
).pack(side="left", padx=(0, 5))

for label_text, var in [("Qty:", multi_qty_var), ("Buy:", multi_buy_var), ("Sell:", multi_sell_var)]:
    ctk.CTkLabel(multi_input_row, text=label_text, text_color=LABEL_COLOR, font=("Segoe UI", 12)).pack(side="left", padx=(5, 2))
    ctk.CTkEntry(multi_input_row, textvariable=var, width=60, **entry_kwargs).pack(side="left")

ctk.CTkButton(
    multi_input_row, text="Add Trade", command=add_multi_trade,
    fg_color="#00d09c", hover_color="#00a87e", text_color="black", font=bold_font, width=90, height=26
).pack(side="right", padx=(10, 0))

scrollable_trades_frame = ctk.CTkScrollableFrame(frame_multi_mode, height=150, fg_color="#121212", border_width=1, border_color=BORDER_COLOR)
scrollable_trades_frame.pack(fill="both", expand=True, pady=5)

multi_footer = ctk.CTkFrame(frame_multi_mode, fg_color="#161616", corner_radius=6)
multi_footer.pack(fill="x", pady=(5, 0))
multi_footer.grid_columnconfigure((0,1,2,3), weight=1)

ctk.CTkLabel(multi_footer, text="Turnover", text_color=LABEL_COLOR, font=("Segoe UI", 11)).grid(row=0, column=0, pady=(5,0))
lbl_m_turnover = ctk.CTkLabel(multi_footer, text="₹0.00", text_color="white", font=bold_font)
lbl_m_turnover.grid(row=1, column=0, pady=(0,5))

ctk.CTkLabel(multi_footer, text="Total Gross", text_color=LABEL_COLOR, font=("Segoe UI", 11)).grid(row=0, column=1, pady=(5,0))
lbl_m_gross = ctk.CTkLabel(multi_footer, text="₹0.00", text_color="white", font=bold_font)
lbl_m_gross.grid(row=1, column=1, pady=(0,5))

ctk.CTkLabel(multi_footer, text="Total Charges", text_color=LABEL_COLOR, font=("Segoe UI", 11)).grid(row=0, column=2, pady=(5,0))
lbl_m_charges = ctk.CTkLabel(multi_footer, text="₹0.00", text_color="white", font=bold_font)
lbl_m_charges.grid(row=1, column=2, pady=(0,5))

ctk.CTkLabel(multi_footer, text="Total Net P&L", text_color="white", font=("Segoe UI", 12, "bold")).grid(row=0, column=3, pady=(5,0))
lbl_m_net = ctk.CTkLabel(multi_footer, text="₹0.00", text_color="#00d09c", font=("Segoe UI", 16, "bold"))
lbl_m_net.grid(row=1, column=3, pady=(0,5))

ctk.CTkButton(
    multi_footer, text="Clear", command=lambda: [multi_trades_list.clear(), update_multi_ui()],
    fg_color="transparent", border_width=1, border_color="#eb5b3c", text_color="#eb5b3c", 
    hover_color="#3b1b1b", width=50, height=20, font=("Segoe UI", 10)
).grid(row=0, column=4, rowspan=2, padx=10)

# Initialize
calculate_single()
calculate_max_qty()
switch_mode() 

root.mainloop()