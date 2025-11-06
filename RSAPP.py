import streamlit as st
import random

def martingale(balance, bet_size, spins):
    results = []
    for spin in range(spins):
        bet = bet_size
        while balance >= bet:
            win = (random.randint(0,36) % 2 == 0 and random.randint(0,36) != 0)
            if win:
                balance += bet
                results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Win', 'Balance': balance})
                break
            else:
                balance -= bet
                results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Loss', 'Balance': balance})
                bet *= 2
                if balance < bet:
                    break
    return results

def paroli(balance, bet_size, spins, prog_limit=3):
    results = []
    win_streak = 0
    bet = bet_size
    for spin in range(spins):
        if balance < bet:
            results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Insufficient funds', 'Balance': balance})
            break
        win = (random.randint(0,36) % 2 == 0 and random.randint(0,36) != 0)
        if win:
            balance += bet
            results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Win', 'Balance': balance})
            win_streak += 1
            if win_streak == prog_limit:
                bet = bet_size
                win_streak = 0
            else:
                bet *= 2
        else:
            balance -= bet
            results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Loss', 'Balance': balance})
            bet = bet_size
            win_streak = 0
    return results

def fibonacci(balance, bet_size, spins):
    fib = [bet_size, bet_size]
    for _ in range(20):
        fib.append(fib[-1] + fib[-2])
    pos = 1
    results = []
    for spin in range(spins):
        bet = fib[pos] if pos < len(fib) else bet_size
        if balance < bet:
            results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Insufficient funds', 'Balance': balance})
            break
        win = (random.randint(0,36) % 2 == 0 and random.randint(0,36) != 0)
        if win:
            balance += bet
            pos = max(pos-2, 1)
            results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Win', 'Balance': balance})
        else:
            balance -= bet
            pos += 1
            results.append({'Spin': spin+1, 'Bet': bet, 'Result': 'Loss', 'Balance': balance})
    return results

st.title("Roulette Strategy Simulator")

strategy = st.selectbox("Choose Strategy", ["Martingale", "Paroli", "Fibonacci"])
balance = st.number_input("Starting Balance", min_value=1, value=500, step=1)
bet_size = st.number_input("Betting Unit Size", min_value=1, value=5, step=1)
spins = st.number_input("Number of Spins", min_value=1, value=50, step=1)
prog_limit = 3
if strategy == "Paroli":
    prog_limit = st.number_input("Paroli Progression Limit", min_value=1, value=3, step=1)

if st.button("Run Simulation"):
    if strategy == "Martingale":
        results = martingale(balance, bet_size, spins)
    elif strategy == "Paroli":
        results = paroli(balance, bet_size, spins, prog_limit)
    else:
        results = fibonacci(balance, bet_size, spins)
    st.write("Simulation Results:")
    st.dataframe(results)
