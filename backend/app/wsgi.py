if __name__ == "__main__":
  import uvicorn
  # Use the module:attr string so --reload works reliably
  uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="warning")