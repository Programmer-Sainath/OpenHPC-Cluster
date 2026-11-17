# Slurm commands used

Each run was submitted as a single-node Slurm job on the 4-node cluster (node01-node04).

## 100000 digits

```bash
sbatch -N1 --job-name=chud100000 --output=chud-100000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 100000"
```

## 200000 digits

```bash
sbatch -N1 --job-name=chud200000 --output=chud-200000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 200000"
```

## 300000 digits

```bash
sbatch -N1 --job-name=chud300000 --output=chud-300000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 300000"
```

## 400000 digits

```bash
sbatch -N1 --job-name=chud400000 --output=chud-400000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 400000"
```

## 500000 digits

```bash
sbatch -N1 --job-name=chud500000 --output=chud-500000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 500000"
```

## 600000 digits

```bash
sbatch -N1 --job-name=chud600000 --output=chud-600000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 600000"
```

## 700000 digits

```bash
sbatch -N1 --job-name=chud700000 --output=chud-700000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 700000"
```

## 800000 digits

```bash
sbatch -N1 --job-name=chud800000 --output=chud-800000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 800000"
```

## 900000 digits

```bash
sbatch -N1 --job-name=chud900000 --output=chud-900000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 900000"
```

## 1000000 digits

```bash
sbatch -N1 --job-name=chud1000000 --output=chud-1000000-%j.out --wrap="hostname; cd ~/jobs/chud && python3 chud_fast.py 1000000"
```

