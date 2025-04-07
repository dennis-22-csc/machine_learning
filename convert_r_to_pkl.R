# Load required library
library(reticulate)  # Allows interaction between R and Python

# Load the .RData file
load("stroke_data.RData")

# Combine all loaded objects into a single list
stroke_data <- list(
  risk_preds = risk_preds,
  riskPredNames = riskPredNames,
  stroke_test = stroke_test,
  stroke_train = stroke_train,
  VC_preds = VC_preds
)

# Save as a .pkl file using reticulate
reticulate::py_save_object(stroke_data, "stroke_data.pkl")
print("Saved as stroke_data.pkl")

