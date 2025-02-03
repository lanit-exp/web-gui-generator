<%def name="get_widget_templ(widget, inner_code)">
    <div class=${widget.name} id=${widget.id_}>
        ${inner_code}
    </div>
</%def>