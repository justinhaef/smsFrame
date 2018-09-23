# smsFrame

This is an article to make your grandmother happy, and who doesn't want to tinker with technology and make their grandmothers happy at the same time?

One of my grandmother's favorite things is to watch her screensaver scroll through all those memories.  Seeing the joy she gets as the memories wash over her as each picture comes up will warm any heart.  But getting those pictures on her screensaver isn't easy, especally since I have her computer running Ubuntu Linux.  *With all the scams targeting the elderly, I recommend having this alternative OS for your loved ones as well.* 

After seeing her light up watching that screensaver countless times, it accured to me that leveraging the technology that I know, I could brighten her day a little more.  If I could have a picture frame in the comfort of her living room scrolling these same pictures, she'd be very happy about that.  I then begain thinking how much of a pain it would be to update these pictures, since I don't live in the same town as my grandma.  

__Raspberry Pi and Twilio to the rescue!__

## Standing on others shoulders

First we'll take what we've learned from this past [Twilio blog post](https://www.twilio.com/blog/2018/05/how-to-receive-and-download-picture-messages-in-python-with-twilio-mms.html) and apply it to our use case.  Ours is a little differet as we'll have Twilio send the webhook to AWS Lambda so that we can download the MMS image to an S3 bucket.  We'll then write a job on our Raspberry Pi to download these images and display them via HDMI to a leftover computer monitor we've setup in our grandma's livingroom.

## First AWS

Our first task that we need to get done is setting up our AWS envoriment, this will involve creating an API Gateway, Two IAM Roles, S3 Bucket and a Lambda function.  There are many tutorials on how to create these but I like to use a Python application called Zappa to do this all quickly for me.  

We need to have a signup page so that a user can login, specify the phone numbers and names of people that are allowed to send messages.  Then the AWS lambda funtion should add folders for each sender.  Then, we should create a DynamoDB table that will get meta data (possible facial recognition) and store that.  So if someone wanted to say "show me grandson x on date y" the system could figure that out.

## random thoughts

CloudFormation should be used to create this enviornment. Then use CodeBuild and CodeDeploy for the pipeline.  I think the front end should be using GatsbyJS keeping it serverless. Use the Cognito to manage users.  On a new user creation, we should create a new entry in the DB for the user.   