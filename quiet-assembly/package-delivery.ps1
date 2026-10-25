$ErrorActionPreference = 'Stop'
$assemblyRoot = $PSScriptRoot
$deliveryPaths = @(
  'index.html', 'design-notes.html', '01-date-line.html', '02-date-corner.html', '03-date-rail.html',
  'screens.css', 'themes.css', 'cards.css', 'fonts.css', 'gallery.css',
  'frames', 'assets', 'licenses', 'README.md', 'design-qa.md', 'server.cjs',
  'studies.json', 'build.mjs', 'event-template.inc',
  'qa/contrast.mjs', 'qa/contrast-results.json', 'qa/event-fidelity.json'
)
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archivePath = Join-Path $assemblyRoot 'quiet-assembly.zip'
if (Test-Path -LiteralPath $archivePath) { Remove-Item -LiteralPath $archivePath }
$archive = [System.IO.Compression.ZipFile]::Open($archivePath, 'Create')
try {
  foreach ($deliveryPath in $deliveryPaths) {
    $deliveryItem = Get-Item -LiteralPath (Join-Path $assemblyRoot $deliveryPath)
    $deliveryFiles = if ($deliveryItem.PSIsContainer) { Get-ChildItem -LiteralPath $deliveryItem.FullName -Recurse -File } else { @($deliveryItem) }
    foreach ($deliveryFile in $deliveryFiles) {
      $entryName = $deliveryFile.FullName.Substring($assemblyRoot.Length + 1).Replace('\', '/')
      [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $deliveryFile.FullName, $entryName, 'Optimal') | Out-Null
    }
  }
} finally { $archive.Dispose() }
Get-Item -LiteralPath $archivePath | Select-Object FullName, Length
