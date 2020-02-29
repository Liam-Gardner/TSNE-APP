# SETUP
Install python
    - remember to let it install pip for package management
Install python extension for vs code
Clone the repo
Set up virtual environment
    - py -3 -m venv .venv
Open a new terminal in vs code
You should see (.venv) in the new terminal
pip install -r requirements.txt
flask run



# t-SNE App

Front end that will guide you through the steps needed to use the t-SNE algorithm to visualise data.

## The Problem

Currently we have to comment out and edit the code to:

1. Supply data
2. Convert categorical to numerical
3. Run the correlation plot
4. Drop highly correlated columns
5. Create subsets to test
6. Run PCA
7. Run elbow plot on each subset
8. Manually edit the columns we pass to t-SNE function in two places - really annoying
9. Repeat all for each subset - not good.

## The Goal:

1. User is asked to supply .csv file
2. Backend converts to pandas dataframe
3. User is shown the dataframe (so they can see what is cat or num) and list of columns with check boxes
4. User is asked to tick categorical columns
5. Backend tries to convert categorical to numerical
6. New dataframe is created

7. Correlation plot is ran on BE
8. FE displays plot

9. User is again shown columns with check boxes
10. User is asked which columns to drop

11. User selects columns to drop
12. New dataframe is created

13. User is redirected to new page with the new dataframe displayed

14. User is asked to pick columns to create first subset
15. User is shown columns with check boxes

16. PCA is run and img stored
17. Redirect to PCA image / or open in new tab

18. Click next for elbow plot visualisation

19. User then inputs elbow plot number

20. T-SNE runs...

## Missing Features

1. Add navigation. Please.
2. Backend can suggest which columns to drop based on correlation greater than 0.5 or greater than -0.5.
3. ~~Embed the plotly correlation html into our web page - so we can add navigation / drop cols checkboxes.~~
4. Extract the checkbox filter logic to one function.
   - it is currently repeated in 3 functions.
   - simplify the filter, for example the cat to num func could probably use pandas to figure out which rows are non-numeric and then run the conversion function.
   - but only if we want all the categorical converted.
5. Create subset
   - need navigation beacuse we need to run this multiple times.
6. Loaders
   - the flash method should be linked up to the template.
7. Try plotly instead of matplotlib on pca / kmeans.
8. Is writing the files the best approach? Investigate...
9. The forms file should be one class that can take in fieldnames and pass the value into whatever field we want.
10. All commented out prints should be displayed as extra info in UI.
11. Display on screen the results of the categorical to numerical, because right now if we see for example "Job": 0, "Job": 1, we are not sure what categories these represent.

- They are ordered alphabetically before being given a number so that is how we know - need to make clear to user
