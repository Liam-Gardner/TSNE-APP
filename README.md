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

11. Backend can suggest which columns to drop based on correlation greater than 0.5 or greater than -0.5
12. User selects columns to drop
13. New dataframe is created

14. User is shown columns with check boxes
15. User is asked to pick columns to create first subset

16. PCA is run and displayed

17. Click next for elbow plot visualisation

18. User then inputs elbow plot number

19. T-SNE runs...
