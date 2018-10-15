import slackweb
import os
from chalice import Chalice
from datetime import datetime

app = Chalice(app_name='aws2slack')


"""
{
    "version": "0",
    "id": "98a0df14-0aa3-41e1-b603-5b27ce3c1431",
    "detail-type": "CodeBuild Build State Change",
    "source": "aws.codebuild",
    "account": "123456789012",
    "time": "2017-07-12T00:42:28Z",
    "region": "us-east-1",
    "resources": [
        "arn:aws:codebuild:us-east-1:123456789012:build/SampleProjectName:6bdced96-e528-485b-a64c-10df867f5f33"
    ],
    "detail": {
        "build-status": "IN_PROGRESS",
        "project-name": "SampleProjectName",
        "build-id": "arn:aws:codebuild:us-east-1:123456789012:build/SampleProjectName:6bdced96-e528-485b-a64c-10df867f5f33",
        "current-phase": "SUBMITTED",
        "current-phase-context": "[]",
        "version": "1"
    }
}
"""
@app.lambda_function(name='aws2slack')
def index(event, context):
    slack = slackweb.Slack(url=os.environ['SLACK_HOOK'])
    if event['source'] == "aws.codebuild":
        att = codebuild_msg(event)
        ret = slack.notify(attachments=att)
    else:
        ret = slack.notify(text="unknown event source")
    return ret


"""
{
    "attachments": [
        {
            "fallback": "AWS codebuild: Project status",
            "color": "#36a64f",
            "pretext": "AWS codebuild",
            "title": "Project Name",
            "title_link": "https://project-link.com/",
            "text": "phase: state",
            "ts": 123456789
        }
    ]
}
"""
def codebuild_msg(cb_event):
    attachments = []
    dt = datetime.strptime(cb_event['time'], '%Y-%m-%dT%H:%M:%SZ')

    attachment = {"fallback": cb_event['detail-type']+" - "+
                              cb_event['detail']['project-name']+": "+
                              cb_event['detail']['build-status'],
                  "color": "#36a64f",
                  "pretext": cb_event['detail-type'],
                  "title": cb_event['detail']['project-name'],
                  "title_link": "https://",
                  "text": "build-status: "+cb_event['detail']['build-status'],
                  "ts": dt.timestamp()}
    attachments.append(attachment)

    return attachments
