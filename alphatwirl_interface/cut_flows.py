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


def cut_flow_with_weighted_counter(cut_flow, cut_flow_summary_filename, weight_attr="weight"):
    from functools import partial

    if weight_attr is None or weight_attr == 1:
        eventSelection = _build_selection(cut_flow)
    else:
        eventSelection = alphatwirl.selection.build_selection(
            path_cfg=cut_flow,
            AllClass=alphatwirl.selection.modules.WeightedCountMaker("all", weight_attr),
            AnyClass=alphatwirl.selection.modules.WeightedCountMaker("any", weight_attr),
            NotClass=alphatwirl.selection.modules.WeightedCountMaker("not", weight_attr)
        )
    resultsCombinationMethod = alphatwirl.collector.ToTupleListWithDatasetColumn(
        summaryColumnNames=('depth', 'class', 'name', 'pass', 'total')
    )
    deliveryMethod = alphatwirl.collector.WriteListToFile(cut_flow_summary_filename)
    collector = alphatwirl.loop.Collector(resultsCombinationMethod, deliveryMethod)
    return [(eventSelection, collector)]


def cut_flow(cut_flow):
    eventSelection = alphatwirl.selection.build_selection(
        path_cfg=cut_flow,
        AllClass=alphatwirl.selection.modules.All,
        AnyClass=alphatwirl.selection.modules.Any,
        NotClass=alphatwirl.selection.modules.Not,
    )

    return to_null_collector_pairs([eventSelection])
