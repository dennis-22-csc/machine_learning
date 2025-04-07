# Load the .RData file
load("stroke_data.RData")

# Define the subfolder name
output_folder <- "stroke_datasets"

# Create the folder if it doesn’t exist
if (!dir.exists(output_folder)) {
  dir.create(output_folder)
}

# Get a list of all objects
all_objects <- ls()

# Loop through all objects
for (obj in all_objects) {
  # Get the object dynamically
  data <- get(obj)
  
  # Check if the object is a data frame
  if (is.data.frame(data)) {
    # Define the file path
    filename <- file.path(output_folder, paste0(obj, ".csv"))
    
    # Save the CSV file
    write.csv(data, filename, row.names = FALSE)
    
    # Print confirmation
    print(paste("Saved:", filename))
  }
}

print("All data frames have been converted to CSV and saved in 'stroke_datasets/' folder.")

