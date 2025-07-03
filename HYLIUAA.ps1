param ([string]$BasePath)
Write-Host $BasePath

$test = "ASD"

function Show-Dialog {
    Add-Type -AssemblyName System.Windows.Forms
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Select Function"
    $form.ShowIcon = $false
    $form.ClientSize = [Drawing.Size]::new(400, 250)
    $form.StartPosition = 'CenterScreen'

    $buttons = @(
        @{Text="功能功能功能功能功能功能A"; Action={ Get_SASEG }},
        @{Text="功能B"; Action={ Write-Host "执行功能B" }},
        @{Text="功能C"; Action={ Write-Host "执行功能C" }},
        @{Text="功能D"; Action={ Write-Host "执行功能D" }}
    )

    $btnHeight = 40
    $spacing = 10
    $btnWidth = [int]($form.ClientSize.Width * 0.8)
    $startY = [int](($form.ClientSize.Height - ($buttons.Count * ($btnHeight + $spacing))) / 2) + $spacing

for ($i=0; $i -lt $buttons.Count; $i++) {
    $btn = New-Object System.Windows.Forms.Button
    $btn.Text = $buttons[$i].Text
    $btn.Size = [Drawing.Size]::new($btnWidth, $btnHeight)
    $btn.Location = [Drawing.Point]::new(
        [int](($form.ClientSize.Width - $btnWidth)/2),
        $startY + $i * ($btnHeight + $spacing)
    )

    $action = $buttons[$i].Action

    $btn.Add_Click({
        & $action
        $form.Close()
    })

    $form.Controls.Add($btn)
}

    $form.Topmost = $true
    $form.ShowDialog() | Out-Null
}

Show-Dialog

$test = "ASD"
function  Get_SASEG {Write-Host "hihihihi $test"}

Get_SASEG