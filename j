# ============================================================
# STEP 1: IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ============================================================
# STEP 2: CREATE A WORKING COPY
# Assumes your raw dataframe is already loaded as df.
# ============================================================

model_df = df.copy()


# ============================================================
# STEP 3: CLEAN THE STAGE FIELD AND CREATE THE TARGET
#
# OPP_STAGENAME is used ONLY to create y:
#   CLOSED WON  = 1
#   CLOSED LOST = 0
#
# It is NOT used as an X feature because it contains the answer.
# ============================================================

model_df["OPP_STAGENAME"] = (
    model_df["OPP_STAGENAME"]
    .fillna("UNKNOWN")
    .astype(str)
    .str.strip()
    .str.upper()
)

model_df = model_df[
    model_df["OPP_STAGENAME"].isin(["CLOSED WON", "CLOSED LOST"])
].copy()

model_df["closed_won"] = np.where(
    model_df["OPP_STAGENAME"] == "CLOSED WON",
    1,
    0
)


# ============================================================
# STEP 4: CLEAN ALL CATEGORICAL FIELDS
#
# This standardizes categories such as:
# "Email", "EMAIL", and " email "
# into the same value.
# ============================================================

categorical_features = [
    "PERSON_ID_TYPE",
    "PERSON_JOB_LEVEL",
    "PERSON_ROLE",
    "BOUNCEBACK",
    "PERSON_GEO",
    "SOURCE_SYSTEM",
    "ACTIVITY_TYPE",
    "ACTIVITY_STATUS",
    "CAMPAIGN_TYPE",
    "CAMPAIGN_CHANNEL",
    "CAMPAIGN_SUB_CHANNEL",
    "JOB_LEVEL_C",
    "JOB_FUNCTION_C"
]

for col in categorical_features:
    model_df[col] = (
        model_df[col]
        .fillna("UNKNOWN")
        .astype(str)
        .str.strip()
        .str.upper()
    )


# ============================================================
# STEP 5: CONVERT DATE FIELDS TO DATETIME
#
# Dates cannot be passed directly into Logistic Regression.
# We convert them first so we can derive numeric timing features.
# ============================================================

date_columns = [
    "PERSON_CREATED_DATE",
    "ACTIVITY_DATE",
    "OPP_CREATE_DATE",
    "OPP_CLOSE_DATE"
]

for col in date_columns:
    model_df[col] = pd.to_datetime(
        model_df[col],
        errors="coerce"
    )


# ============================================================
# STEP 6: CREATE NUMERIC DATE FEATURES
#
# These describe the record at the time of activity.
#
# OPP_CLOSE_DATE is not used as an X feature. It is used only
# for the chronological train/test split later.
# ============================================================

model_df["opportunity_age_days"] = (
    model_df["ACTIVITY_DATE"] - model_df["OPP_CREATE_DATE"]
).dt.days

model_df["person_age_days"] = (
    model_df["ACTIVITY_DATE"] - model_df["PERSON_CREATED_DATE"]
).dt.days

model_df["activity_month"] = model_df["ACTIVITY_DATE"].dt.month

model_df["activity_day_of_week"] = model_df["ACTIVITY_DATE"].dt.dayofweek

# Remove impossible date differences.
model_df.loc[
    model_df["opportunity_age_days"] < 0,
    "opportunity_age_days"
] = np.nan

model_df.loc[
    model_df["person_age_days"] < 0,
    "person_age_days"
] = np.nan


# ============================================================
# STEP 7: DEFINE THE FINAL X FEATURES
#
# Included:
# - Campaign type/channel/sub-channel
# - Activity type/status
# - Bounceback
# - Person/context categories
# - Derived date features
#
# Excluded:
# - EMAIL: nearly unique identifier
# - PERSON_ID: identifier
# - PERSON_TITLE: too granular/high-cardinality initially
# - CAMPAIGNID: identifier
# - ACCOUNT_ID: identifier
# - OPP_STAGENAME: target source
# - OPP_CLOSE_DATE: future information
# ============================================================

categorical_x_features = [
    "PERSON_ID_TYPE",
    "PERSON_JOB_LEVEL",
    "PERSON_ROLE",
    "BOUNCEBACK",
    "PERSON_GEO",
    "SOURCE_SYSTEM",
    "ACTIVITY_TYPE",
    "ACTIVITY_STATUS",
    "CAMPAIGN_TYPE",
    "CAMPAIGN_CHANNEL",
    "CAMPAIGN_SUB_CHANNEL",
    "JOB_LEVEL_C",
    "JOB_FUNCTION_C"
]

numeric_x_features = [
    "opportunity_age_days",
    "person_age_days",
    "activity_month",
    "activity_day_of_week"
]

feature_columns = categorical_x_features + numeric_x_features

X = model_df[feature_columns].copy()

y = model_df["closed_won"].copy()


# ============================================================
# STEP 8: CREATE A TIME-BASED TRAIN/TEST SPLIT
#
# Older closed opportunities train the model.
# Newer closed opportunities test the model.
#
# OPP_CLOSE_DATE is used for ordering only, never as a predictor.
# ============================================================

split_df = model_df[
    ["OPP_CLOSE_DATE", "closed_won"] + feature_columns
].dropna(subset=["OPP_CLOSE_DATE"]).copy()

split_df = split_df.sort_values("OPP_CLOSE_DATE")

split_index = int(len(split_df) * 0.70)

train_df = split_df.iloc[:split_index].copy()
test_df = split_df.iloc[split_index:].copy()

X_train = train_df[feature_columns]
X_test = test_df[feature_columns]

y_train = train_df["closed_won"]
y_test = test_df["closed_won"]


# ============================================================
# STEP 9: PREPARE THE FEATURES
#
# Categorical fields:
# - Fill missing values with UNKNOWN
# - Convert categories into dummy variables
#
# Numeric fields:
# - Fill missing values with the training median
# - Standardize values for Logistic Regression
# ============================================================

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),
        (
            "one_hot_encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical_features",
            categorical_transformer,
            categorical_x_features
        ),
        (
            "numeric_features",
            numeric_transformer,
            numeric_x_features
        )
    ]
)


# ============================================================
# STEP 10: BUILD AND FIT THE LOGISTIC REGRESSION MODEL
#
# class_weight="balanced" is helpful when Closed Lost is much
# more common than Closed Won.
# ============================================================

logistic_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "logistic_regression",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=1
            )
        )
    ]
)

logistic_model.fit(
    X_train,
    y_train
)


# ============================================================
# STEP 11: CREATE WIN PROBABILITIES AND 0-100 MODEL SCORES
#
# Example:
# 0.63 predicted probability = 63 model score
# ============================================================

predicted_class = logistic_model.predict(X_test)

predicted_win_probability = logistic_model.predict_proba(X_test)[:, 1]

model_score_0_to_100 = np.round(
    predicted_win_probability * 100,
    0
).astype(int)


# ============================================================
# STEP 12: EVALUATE MODEL PERFORMANCE
# ============================================================

print("\nClassification Report:\n")
print(
    classification_report(
        y_test,
        predicted_class
    )
)

print("\nConfusion Matrix:\n")
print(
    confusion_matrix(
        y_test,
        predicted_class
    )
)

print("\nROC-AUC Score:\n")
print(
    round(
        roc_auc_score(
            y_test,
            predicted_win_probability
        ),
        3
    )
)


# ============================================================
# STEP 13: REVIEW SCORED RESULTS
#
# This shows how the model scored the most recent test-period data.
# ============================================================

results = X_test.copy()

results["actual_closed_won"] = y_test.values
results["predicted_win_probability"] = predicted_win_probability
results["model_score_0_to_100"] = model_score_0_to_100

results = results.sort_values(
    "model_score_0_to_100",
    ascending=False
)

print("\nTop 20 Highest-Scored Records:\n")
print(
    results[
        [
            "actual_closed_won",
            "predicted_win_probability",
            "model_score_0_to_100"
        ]
    ].head(20)
)


# ============================================================
# STEP 14: VIEW MODEL COEFFICIENTS
#
# Positive coefficient:
# Associated with higher odds of Closed Won.
#
# Negative coefficient:
# Associated with lower odds of Closed Won.
# ============================================================

feature_names = logistic_model.named_steps[
    "preprocessor"
].get_feature_names_out()

coefficients = logistic_model.named_steps[
    "logistic_regression"
].coef_[0]

coefficient_table = pd.DataFrame(
    {
        "feature": feature_names,
        "coefficient": coefficients,
        "odds_ratio": np.exp(coefficients)
    }
).sort_values(
    "coefficient",
    ascending=False
)

print("\nFeatures Most Associated With Closed Won:\n")
print(coefficient_table.head(20))

print("\nFeatures Most Associated With Closed Lost:\n")
print(coefficient_table.tail(20))
