from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# serve CSS later if you want
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse, name="submit_form")
async def submit_form(
    request: Request,
    project_name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    server_size: str = Form(...),
    description: str = Form(...),
    base_os: str = Form(...),
    optional_software: list[str] = Form([]),
    disk_size: str = Form(...),
    disk_unit: str = Form(...),
    mount_path: str = Form(...),
):
        # format the email body
    body = f"""
    Server Request Submitted:

    Project: {project_name}
    Start: {start_date} → End: {end_date}
    Server Size: {server_size}
    Description: {description}
    Base OS: {base_os}
    Optional Software: {', '.join(optional_software) if optional_software else 'None'}
    Disk: {disk_size} {disk_unit}
    Mount Path: {mount_path}
    """

    msg = MIMEText(body)
    msg["Subject"] = f"New Server Request: {project_name}"
    msg["From"] = "nmacgreg@ualberta.ca"
    msg["To"] = "nmacgreg@ualberta.ca"
    msg["Date"] = formatdate(localtime=True)

    # hand off to local postfix
    with smtplib.SMTP("localhost") as smtp:
        smtp.send_message(msg)

    return templates.TemplateResponse(
        "submitted.html",
        {
            "request": request,
            "project_name": project_name,
            "start_date": start_date,
            "end_date": end_date,
            "server_size": server_size,
            "description": description,
            "base_os": base_os,
            "optional_software": optional_software,
            "disk_size": f"{disk_size} {disk_unit}",
            "mount_path": mount_path,
        },
    )

