from xmlrpclib import ServerProxy

if __name__ == "__main__":
    s = ServerProxy("http://localhost:7080")
    print s.add(1, 2)
    print s.echo("hello")
    print s.AddCard("34224", 0)
    print s.SetBalance("34224", 5)
    print s.GetBalance("34224")
    print s.IncBalance("34224", 2)
    print s.DecBalance("34224", 1)