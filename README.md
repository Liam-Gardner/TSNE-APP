# t-SNE App

Front end that will guide you through the steps needed to use the t-SNE algorithm to visualise data.

## Currently we have to comment out and edit the code to

1. Supply data
2. Convert categorical to numerical
3. Run the correlation plot
4. Drop highly correlated columns
5. Create subsets to test
6. Run PCA
7. Run elbow plot on each subset
8. Manually edit the columns we pass to t-SNE function in two places - really fucking annoying
9. Repeat all for each subset - ridiculous

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

12.1 User is redirected to new page with the new dataframe displayed

13. User is asked to pick columns to create first subset
14. User is shown columns with check boxes

15. PCA is run and img stored
    15.1 Redirect to PCA image / or open in new tab

16. Click next for elbow plot visualisation

17. User then inputs elbow plot number

18. T-SNE runs...

## Extras

1. Add navigation
2. Backend can suggest which columns to drop based on correlation greater than 0.5 or greater than -0.5
3. Embed the plotly correlation html into our web page
   - so we can add navigation / drop cols checkboxes
4. Extract the checkbox filter logic ro one function
   - it is currently repeated in 3 functions
   - simplify the filter, for example the cat to num func could probably use pandas to figure out which rows are non-numeric and the run the conversion function
     - that's if we want all the categorical converted
5. Create subset
   - need navigation beacuse we need to run this multiple times
6. Loaders
   - the flash method should be linked up to the template
7. Use plotly instead of matplotlib on pca / kmeans / t-sne
8. Is writing the file neccessary each time? Can't we do something in memory? Or database?
9. The forms file should be one class that can take in fieldnames and pass the value into whatever field we want - tried it already but failed, try again!
10. All commented out prints should be displayed as extra info in UI
11. Do not allow dots in the input box for subset names, in the tsne function we split on dot to remove the file extension and name the tsne files. Probably no big deal as we would just end up with something like "t-SNE-personal.csv.html"
