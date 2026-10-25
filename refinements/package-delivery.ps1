$ErrorActionPreference = 'Stop'
$studyRoot = $PSScriptRoot
$deliveryPaths = @(
  'index.html', 'design-notes.html',
  '01-soft-focus.html', '02-humanist.html', '03-warm-editorial.html',
  '04-open-form.html', '05-studio-notes.html', '06-quiet-air.html',
  'screens.css', 'themes.css', 'fonts.css', 'gallery.css',
  'frames', 'assets', 'licenses', 'README.md', 'design-qa.md', 'server.cjs', 'studies.json'
)
$resolvedDeliveryPaths = foreach ($deliveryPath in $deliveryPaths) {
  Join-Path $studyRoot $deliveryPath
}
Compress-Archive -LiteralPath $resolvedDeliveryPaths -DestinationPath (Join-Path $studyRoot 'quiet-studies.zip') -Force
Get-Item -LiteralPath (Join-Path $studyRoot 'quiet-studies.zip') | Select-Object FullName, Length
