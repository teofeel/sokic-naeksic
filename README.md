Install all required packages:
```powershell
pip install -r requirements.txt
```

Install required plugins and components:

```powershell
pip install ./api ./core ./plugins/data_source_plugin_yaml ./plugins/data_source_plugin_json ./plugins/block_visualizer ./plugins/simple_visualizer
```

To ensure the Graph and Bird View render correctly you must include the global stylesheet in HTML head
```html
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
```

You can generate graph with:
Windows:
```powershell
python graph_generator.py
```
Linux:
```terminal
python3 graph_generator.py
```


