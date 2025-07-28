
import streamlit as st
from itertools import combinations, permutations

st.title("Pipe Cutting Optimizer")
st.markdown("Minimize waste by choosing optimal cut assignments.")

# Input UI
required_input = st.text_input("Enter required cuts (e.g., 32x1,68x1,18x1)", "32x1,68x1,18x1")
stock_input = st.text_input("Enter stock pipes (e.g., 96x1,120x1,144x1)", "96x1,120x1,144x1")

def parse_input(input_str):
    items = input_str.split(",")
    result = []
    for item in items:
        if "x" in item:
            length, qty = item.split("x")
            result.append((int(length), int(qty)))
    return result

required_cuts = parse_input(required_input)
stock_pipes = parse_input(stock_input)

# Expand required cuts and stock list
cuts_list = []
for length, qty in required_cuts:
    cuts_list.extend([length] * qty)

stock_list = []
for length, qty in stock_pipes:
    stock_list.extend([length] * qty)

# Cutting logic
def try_assignment(cuts, stocks):
    results = []
    remaining_cuts = cuts[:]
    for stock in stocks:
        best_combo = None
        best_waste = stock
        for r in range(1, len(remaining_cuts) + 1):
            for combo in combinations(remaining_cuts, r):
                if sum(combo) <= stock:
                    waste = stock - sum(combo)
                    if waste < best_waste:
                        best_combo = combo
                        best_waste = waste
                        if waste == 0:
                            break
        if best_combo:
            results.append((stock, best_combo, best_waste))
            for cut in best_combo:
                remaining_cuts.remove(cut)
        else:
            results.append((stock, (), stock))  # Unused
    total_waste = sum(r[2] for r in results)
    return results, total_waste

# Find best plan
best_result = None
min_waste = float('inf')

for perm in permutations(stock_list):
    layout, waste = try_assignment(cuts_list, list(perm))
    if waste < min_waste:
        best_result = layout
        min_waste = waste

# Output result
st.subheader("Best Cutting Plan")
for pipe_len, cuts, waste in best_result:
    st.write(f"Pipe {pipe_len}: cuts {list(cuts)} → waste {waste}")
st.success(f"Total Waste: {min_waste}")
