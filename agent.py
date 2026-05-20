import pandas as pd

# -----------------------------
# LOAD DATA SAFELY
# -----------------------------
try:
    leave_df = pd.read_excel("leave-tracker.xlsx")
    capacity_df = pd.read_excel("capacity-planner.xlsx")
    dependency_df = pd.read_excel("dependency-matrix.xlsx")
    print("✅ Data Loaded Successfully\n")
except Exception as e:
    print(f"❌ Error loading files: {e}")
    exit()

# -----------------------------
# LEAVE CONFLICT ANALYSIS
# -----------------------------
print("🔍 LEAVE CONFLICTS:")
try:
    grouped = leave_df.groupby("Date")

    conflict_found = False
    for date, group in grouped:
        if len(group) > 1:
            names = ", ".join(group["Name"].astype(str))
            print(f"⚠️ {date}: {names} are on leave (High Risk)")
            conflict_found = True

    if not conflict_found:
        print("✅ No leave conflicts detected")

except Exception as e:
    print(f"⚠️ Error analyzing leave data: {e}")

# -----------------------------
# CAPACITY ANALYSIS
# -----------------------------
print("\n🔍 CAPACITY GAPS:")
try:
    overload_found = False

    for index, row in capacity_df.iterrows():
        if row["Allocated Work"] > row["Available Hours"]:
            print(f"⚠️ {row['Name']} overloaded ({row['Allocated Work']} > {row['Available Hours']})")
            overload_found = True

    if not overload_found:
        print("✅ No capacity issues detected")

except Exception as e:
    print(f"⚠️ Error analyzing capacity data: {e}")

# -----------------------------
# DEPENDENCY RISK ANALYSIS
# -----------------------------
print("\n🔍 DEPENDENCY RISKS:")
try:
    risk_found = False

    for index, row in dependency_df.iterrows():
        if pd.isna(row["Backup Resource"]) or row["Backup Resource"] == "":
            print(f"⚠️ {row['Task']} has no backup (Owner: {row['Primary Owner']})")
            risk_found = True

    if not risk_found:
        print("✅ No dependency risks detected")

except Exception as e:
    print(f"⚠️ Error analyzing dependency data: {e}")

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
print("\n💡 RECOMMENDATIONS:")
print("- Avoid overlapping leave for critical team members")
print("- Ensure every critical task has a backup resource")
print("- Balance workload across team members")
print("- Plan sprint capacity based on actual availability")

# -----------------------------
# END
# -----------------------------
print("\n✅ ANALYSIS COMPLETE")
