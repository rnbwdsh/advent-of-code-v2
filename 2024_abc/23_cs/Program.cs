﻿class Program
{
    private const int MaxCliqueSize = 3;
    private const int NoMaxSize = -1;

    static void Main(string[] args)
    {
        var example = "kh-tc\nqp-kh\nde-cg\nka-co\nyn-aq\nqp-ub\ncg-tb\nvc-aq\ntb-ka\nwh-tc\nyn-cg\nkh-ub\nta-co\nde-co\ntc-td\ntb-wq\nwh-td\nta-ka\ntd-qp\naq-cg\nwq-ub\nub-vc\nde-ta\nwq-aq\nwq-vc\nwh-yn\nka-de\nkh-ta\nco-tc\nwh-qp\ntb-vc\ntd-yn".Split("\n").ToList();
        ProcessData(example);
        ProcessData(File.ReadAllLines("23.in").ToList());
    }

    static void ProcessData(List<string> data)
    {
        var graph = BuildGraph(data);

        var cliquesOfSizeThreeStartingWithT = GetCliques(graph, MaxCliqueSize)
            .Where(c => c.Any(node => node.StartsWith("t")))
            .Where(c => c.Count == MaxCliqueSize)
            .ToHashSet();
        Console.WriteLine("A: " + cliquesOfSizeThreeStartingWithT.Count);

        var longestCliqueSorted = GetCliques(graph)
            .OrderByDescending(clique => clique.Count)
            .First()
            .OrderBy(node => node)
            .ToList();
        Console.WriteLine("B: " + string.Join(",", longestCliqueSorted));
    }

    static Dictionary<string, List<string>> BuildGraph(List<string> data)
    {
        var graph = new Dictionary<string, List<string>>();
        foreach (var line in data)
        {
            var parts = line.Split('-');
            AddEdgeToGraph(graph, parts[0], parts[1]);
            AddEdgeToGraph(graph, parts[1], parts[0]);
        }
        return graph;
    }

    static void AddEdgeToGraph(Dictionary<string, List<string>> graph, string key, string value)
    {
        if (!graph.ContainsKey(key))
        {
            graph[key] = [];
        }
        graph[key].Add(value);
    }

    static HashSet<HashSet<string>> GetCliques(Dictionary<string, List<string>> graph, int maxSize=NoMaxSize)
    {
        var setOfSets = new HashSet<HashSet<string>>(HashSet<string>.CreateSetComparer());
        var sortedKeys = graph.Keys.OrderBy(key => key).ToList();
        FindAllCliques(graph, [], sortedKeys, setOfSets, maxSize);
        return setOfSets;
    }

    private static void FindAllCliques(Dictionary<string, List<string>> graph, List<string> clique, List<string> candidates, HashSet<HashSet<string>> result, int maxSize)
    {
        if ((candidates.Count == 0 && maxSize == NoMaxSize) || clique.Count == maxSize)
        {
            result.Add([.. clique]);
            return;
        }

        foreach (var candidate in candidates)
        {
            var newClique = new List<string>(clique) { candidate };
            var newCandidates = candidates
                .Where(c => graph[c].Contains(candidate))
                .Where(c => c.CompareTo(candidate) > 0)
                .ToList();
            FindAllCliques(graph, newClique, newCandidates, result, maxSize);
        }
    }
}