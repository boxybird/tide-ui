$ErrorActionPreference = 'Stop'
$practiceRoot = $PSScriptRoot
$deliveryPaths = @(
  'index.html', 'baseline.html', 'local-partner.html', 'rough-upload.html', 'partner.html', 'design-notes.html',
  'screens.css', 'cards.css', 'themes.css', 'fonts.css', 'gallery.css', 'reality.css', 'presentation.css',
  'frames', 'assets', 'licenses', 'source', 'README.md', 'design-qa.md', 'server.cjs', 'build.mjs', 'studies.json', 'baseline-lock.json',
  'qa/contrast.mjs', 'qa/contrast-results.json', 'qa/preservation-results.json', 'qa/browser-metrics-390.json'
)
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archivePath = Join-Path $practiceRoot 'date-line-in-practice.zip'
if (Test-Path -LiteralPath $archivePath) { Remove-Item -LiteralPath $archivePath }
$archive = [System.IO.Compression.ZipFile]::Open($archivePath, 'Create')
try {
  foreach ($deliveryPath in $deliveryPaths) {
    $deliveryItem = Get-Item -LiteralPath (Join-Path $practiceRoot $deliveryPath)
    $deliveryFiles = if ($deliveryItem.PSIsContainer) { Get-ChildItem -LiteralPath $deliveryItem.FullName -Recurse -File } else { @($deliveryItem) }
    foreach ($deliveryFile in $deliveryFiles) {
      $entryName = $deliveryFile.FullName.Substring($practiceRoot.Length + 1).Replace('\', '/')
      [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $deliveryFile.FullName, $entryName, 'Optimal') | Out-Null
    }
  }
} finally { $archive.Dispose() }
Get-Item -LiteralPath $archivePath | Select-Object FullName, Length
