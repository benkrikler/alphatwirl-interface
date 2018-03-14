import alphatwirl
from alphatwirl_interface.completions import to_null_collector_pairs


def _build_selection(cut_flow):
    return alphatwirl.selection.build_selection(
        path_cfg=cut_flow,
        AllClass=alphatwirl.selection.modules.AllwCount,
        AnyClass=alphatwirl.selection.modules.AnywCount,
        NotClass=alphatwirl.selection.modules.NotwCount
    )


def _file_collector(cut_flow_summary_filename):
    resultsCombinationMethod = alphatwirl.collector.ToTupleListWithDatasetColumn(
        summaryColumnNames=('depth', 'class', 'name', 'pass', 'total')
    )
    deliveryMethod = alphatwirl.collector.WriteListToFile(
        cut_flow_summary_filename)
    collector = alphatwirl.loop.Collector(
        resultsCombinationMethod, deliveryMethod)
    return collector


def cut_flow_with_counter(cut_flow, cut_flow_summary_filename):
    eventSelection = _build_selection(cut_flow)
    collector = _file_collector(cut_flow_summary_filename)

    return [(eventSelection, collector)]


def cut_flow(cut_flow):
    eventSelection = _build_selection(cut_flow)

    return to_null_collector_pairs([eventSelection])
