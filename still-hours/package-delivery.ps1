$ErrorActionPreference = 'Stop'
$stillRoot = $PSScriptRoot
$deliveryPaths = @(
  'index.html', 'design-notes.html',
  '01-sage.html', '02-bookish.html', '03-soft-margin.html',
  '04-field-notes.html', '05-umber.html', '06-hushed.html',
  'screens.css', 'themes.css', 'fonts.css', 'gallery.css',
  'frames', 'assets', 'licenses', 'README.md', 'design-qa.md',
  'server.cjs', 'studies.json', 'build.mjs', 'notes.mjs', 'detail-content.inc',
  'qa/contrast.mjs', 'qa/contrast-results.json'
)
$resolvedDeliveryPaths = foreach ($deliveryPath in $deliveryPaths) {
  Join-Path $stillRoot $deliveryPath
}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archivePath = Join-Path $stillRoot 'still-hours.zip'
if (Test-Path -LiteralPath $archivePath) { Remove-Item -LiteralPath $archivePath }
$archive = [System.IO.Compression.ZipFile]::Open($archivePath, 'Create')
try {
  foreach ($deliveryPath in $resolvedDeliveryPaths) {
    $deliveryItem = Get-Item -LiteralPath $deliveryPath
    $deliveryFiles = if ($deliveryItem.PSIsContainer) { Get-ChildItem -LiteralPath $deliveryPath -Recurse -File } else { @($deliveryItem) }
    foreach ($deliveryFile in $deliveryFiles) {
      $entryName = $deliveryFile.FullName.Substring($stillRoot.Length + 1).Replace('\', '/')
      [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $deliveryFile.FullName, $entryName, 'Optimal') | Out-Null
    }
  }
} finally { $archive.Dispose() }
Get-Item -LiteralPath (Join-Path $stillRoot 'still-hours.zip') | Select-Object FullName, Length
