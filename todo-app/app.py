from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

tasks = []

@app.route("/")
def index():
    visible_tasks = [t for t in tasks if t["status"] != "deleted"]
    return render_template("index.html", tasks=visible_tasks)


@app.route("/add", methods=["POST"])
def add_task():
    text = request.form.get("task")
    due_date = request.form.get("due_date")
    priority = request.form.get("priority")

    if text:
        tasks.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "due_date": due_date,
            "priority": priority,
            "status": "pending"
        })

    return redirect(url_for("index"))


@app.route("/status/<task_id>/<new_status>", methods=["POST"])
def change_status(task_id, new_status):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            break
    return redirect(url_for("index"))
