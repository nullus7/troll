spawn(function() 
    repeat
        task.wait()
    until game:IsLoaded()
    repeat
        task.wait()
    until game.Players
    repeat
        task.wait()
    until game.Players.LocalPlayer and game.Players.LocalPlayer.Team ~= nil 
    wait(1.5)
    require(game.ReplicatedStorage.Notification).new("<Color=Red>Ang Pogi Ni Mist<Color=/>"):Display()
    wait(.5)
    require(game.ReplicatedStorage.Notification).new("<Color=Red>Ang Pogi Ni Mist<Color=/>"):Display()
    wait(.14)
    require(game.ReplicatedStorage.Notification).new("<Color=Yellow>Ang Pogi Ni Mist<Color=/>"):Display()
    wait(.24)
    require(game.ReplicatedStorage.Notification).new("<Color=Yellow>POGI HUB<Color=/>"):Display()
    wait(.29)
    require(game.ReplicatedStorage.Notification).new("<Color=Yellow>https://inote.pro/notes/E9V412<Color=/>"):Display()
    wait(.36)
end)