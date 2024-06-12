from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Entry


@app.route("/")
def index():
    entries = Entry.query.all()
    return render_template("index.html", entries=entries)


@app.route("/entry/<int:entry_id>")
def view_entry(entry_id):
    entries = Entry.query.all()
    entry = Entry.query.get_or_404(entry_id)
    return render_template("view_entry.html", entry=entry, entries=entries)


@app.route("/entry/new", methods=["GET", "POST"])
def new_entry():
    entries = Entry.query.all()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_entry = Entry(title=title, content=content)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_entry.html", entries=entries)


@app.route("/entry/<int:entry_id>/edit", methods=["GET", "POST"])
def edit_entry(entry_id):
    entries = Entry.query.all()
    entry = Entry.query.get_or_404(entry_id)
    if request.method == "POST":
        entry.title = request.form["title"]
        entry.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("view_entry", entry_id=entry.id))
    return render_template("edit_entry.html", entry=entry, entries=entries)


@app.route("/entry/<int:entry_id>/delete", methods=["POST"])
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("index"))
