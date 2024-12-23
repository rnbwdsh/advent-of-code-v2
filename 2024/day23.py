from typing import List

import networkx
import networkx as nx
import pytest


@pytest.mark.data('kh-tc\nqp-kh\nde-cg\nka-co\nyn-aq\nqp-ub\ncg-tb\nvc-aq\ntb-ka\nwh-tc\nyn-cg\nkh-ub\nta-co\nde-co\ntc-td\ntb-wq\nwh-td\nta-ka\ntd-qp\naq-cg\nwq-ub\nub-vc\nde-ta\nwq-aq\nwq-vc\nwh-yn\nka-de\nkh-ta\nco-tc\nwh-qp\ntb-vc\ntd-yn', 7, "co,de,ka,ta")
def test_23(data: List[str], level):
    g = networkx.Graph([line.split('-') for line in data])
    if level:
        clique_size = {len(c): c for c in nx.find_cliques(g)}
        return ",".join(sorted(clique_size[max(clique_size.keys())]))
    else:
        return len([c for c in nx.enumerate_all_cliques(g)
                    if len(c) == 3 and any(cc.startswith("t") for cc in c)])
