{{- define "stayledger.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "stayledger.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name (include "stayledger.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "stayledger.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "stayledger.labels" -}}
helm.sh/chart: {{ include "stayledger.chart" . }}
app.kubernetes.io/name: {{ include "stayledger.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "stayledger.selectorLabels" -}}
app.kubernetes.io/name: {{ include "stayledger.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
