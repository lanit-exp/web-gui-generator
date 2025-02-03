## lwindow

<%!
    from web_gui_generator.model.wo_abc import AtomicWOMixin
%>
<%
    lookup = context["lookup"]
    def dfs(node):
        inner_code = ""
        if not isinstance(node, AtomicWOMixin):
            for child in node.children:
                 inner_code += dfs(child)
        return lookup.get_template(f"{node.name}.mako").get_def("get_widget_templ").render(widget=node, inner_code=inner_code)
%>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="${css_file}">
    <title>abc></title>
</head>

<body>

<div id=${root_node.id_} class="LWindow">
% for child in root_node.children:
    <%block>
        ${dfs(child)}
    </%block>
% endfor
</div>

</body>  
</html>