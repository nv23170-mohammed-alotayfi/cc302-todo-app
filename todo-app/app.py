from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

tasks = []

@app.route("/")
def index():
    todo_tasks = [t for t in tasks if t["status"] == "pending"]
    done_tasks = [t for t in tasks if t["status"] == "done"]
    return render_template(
        "index.html",
        todo_tasks=todo_tasks,
        done_tasks=done_tasks
    )

@app.route("/add", methods=["POST"])
def add_task():
    text = request.form.get("task")
    if text:
        tasks.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "status": "pending"
        })
    return redirect(url_for("index"))

@app.route("/done/<task_id>", methods=["POST"])
def mark_done(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
    return redirect(url_for("index"))

@app.route("/edit/<task_id>", methods=["POST"])
def edit_task(task_id):
    new_text = request.form.get("new_text")
    if new_text:  # Only update if not empty
        for task in tasks:
            if task["id"] == task_id:
                task["text"] = new_text
                break
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
