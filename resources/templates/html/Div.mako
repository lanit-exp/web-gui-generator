<%def name="get_widget_templ(widget, inner_code)">
    <div id=${widget.id_} class=${widget.name}>
        ${inner_code}
    </div>
</%def>